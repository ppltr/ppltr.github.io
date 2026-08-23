#!/usr/bin/env bash
# Google ile giriş + bulut yedeği için Firebase kurulumu.
#
# CLI'nin yapabildiği her şeyi yapar; konsoldan elle yapılması gereken iki adımı
# sonda yazar. Yeniden çalıştırmak güvenlidir: var olanı bulur, üstüne yazmaz.
#
#   ./scripts/setup_firebase.sh                 → yeni proje sorar ya da seçtirir
#   ./scripts/setup_firebase.sh <proje-id>      → var olan projeyi kullanır
#
# Çıktı: web/firebase-config.json  (herkese açık olması normaldir, sır değildir —
# güvenlik firestore.rules ile sağlanır)

set -euo pipefail
cd "$(dirname "$0")/.."

KIRMIZI=$'\033[31m'; YESIL=$'\033[32m'; SARI=$'\033[33m'; KALIN=$'\033[1m'; BITIR=$'\033[0m'
adim(){ printf "\n%s▸ %s%s\n" "$KALIN" "$1" "$BITIR"; }
uyar(){ printf "%s! %s%s\n" "$SARI" "$1" "$BITIR"; }
hata(){ printf "%s✗ %s%s\n" "$KIRMIZI" "$1" "$BITIR"; exit 1; }
tamam(){ printf "%s✓ %s%s\n" "$YESIL" "$1" "$BITIR"; }

command -v firebase >/dev/null || hata "firebase CLI yok. Kur: npm i -g firebase-tools"
command -v python3  >/dev/null || hata "python3 gerekli"

adim "Firebase oturumu"
if ! firebase login:list 2>/dev/null | grep -q "Logged in"; then
  firebase login
fi
tamam "$(firebase login:list 2>/dev/null | sed -n 's/.*Logged in as //p' | head -1)"

# ── Proje ───────────────────────────────────────────────────────────
PROJE="${1:-}"
if [ -z "$PROJE" ]; then
  adim "Proje"
  firebase projects:list
  printf "\nKullanılacak proje ID (yeni açmak için boş bırak): "
  read -r PROJE
fi

if [ -z "$PROJE" ]; then
  printf "Yeni proje ID (küçük harf, tire; ör. ppl-soru-bankasi): "
  read -r PROJE
  [ -n "$PROJE" ] || hata "proje ID boş olamaz"
  firebase projects:create "$PROJE" --display-name "PPL Soru Bankasi" \
    || hata "proje açılamadı (ID alınmış olabilir)"
fi
tamam "proje: $PROJE"

# ── Web uygulaması ──────────────────────────────────────────────────
adim "Web uygulaması"
# --json çıktısı tablo biçiminden çok daha güvenilir
app_id(){
  firebase apps:list WEB --project "$PROJE" --json 2>/dev/null | python3 -c '
import json, sys
try: d = json.load(sys.stdin)
except Exception: sys.exit(0)
for a in (d.get("result") or []):
    if a.get("appId"):
        print(a["appId"]); break
'
}
APP_ID="$(app_id)"
if [ -z "$APP_ID" ]; then
  firebase apps:create WEB "PPL Calisma" --project "$PROJE" >/dev/null 2>&1 || true
  APP_ID="$(app_id)"
  [ -n "$APP_ID" ] || hata "web uygulaması oluşturulamadı"
  tamam "web uygulaması açıldı"
else
  tamam "var olan web uygulaması kullanılıyor"
fi

# ── Yapılandırma ────────────────────────────────────────────────────
adim "Yapılandırma yazılıyor"
firebase apps:sdkconfig WEB "$APP_ID" --project "$PROJE" --json 2>/dev/null \
  > /tmp/ppl-fbconf.json || hata "SDK yapılandırması alınamadı"
python3 - <<'PY'
import json, sys, pathlib
try:
    d = json.loads(pathlib.Path("/tmp/ppl-fbconf.json").read_text(encoding="utf-8"))
except Exception:
    sys.exit("hata: SDK yapılandırması okunamadı")
conf = d.get("result", d)
conf = conf.get("sdkConfig", conf)
gerek = ["apiKey", "authDomain", "projectId", "appId"]
eksik = [k for k in gerek if not conf.get(k)]
if eksik:
    sys.exit("hata: yapılandırmada eksik alan: " + ", ".join(eksik))
out = {k: conf[k] for k in
       ("apiKey", "authDomain", "projectId", "storageBucket",
        "messagingSenderId", "appId") if conf.get(k)}
p = pathlib.Path("web/firebase-config.json")
p.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("  web/firebase-config.json  ·  " + out["projectId"])
PY
tamam "yapılandırma hazır"

# ── Firestore ───────────────────────────────────────────────────────
adim "Firestore veritabanı"
if firebase firestore:databases:list --project "$PROJE" 2>/dev/null | grep -q "(default)"; then
  tamam "veritabanı zaten var"
else
  firebase firestore:databases:create "(default)" --location=eur3 --project "$PROJE" \
    && tamam "veritabanı açıldı (eur3)" \
    || uyar "veritabanı açılamadı — konsoldan Firestore'u başlat, sonra bu betiği tekrar çalıştır"
fi

adim "Güvenlik kuralları yayımlanıyor"
firebase deploy --only firestore:rules --project "$PROJE" \
  && tamam "kurallar yayında" \
  || uyar "kurallar yayımlanamadı — Firestore açıldıktan sonra tekrar dene"

# ── İzinli alan ─────────────────────────────────────────────────────
# Authentication bir kez konsoldan açıldıktan sonra izinli alan listesi admin
# API'siyle güncellenebiliyor. CLI'nin kendi oturum belirteci kullanılır.
adim "İzinli alanlar"
SITE="${SITE_ALAN:-ppltr.github.io}"
TOKEN="$(python3 -c "import json,pathlib;p=pathlib.Path.home()/'.config/configstore/firebase-tools.json';print(json.loads(p.read_text())['tokens']['access_token'] if p.exists() else '')" 2>/dev/null)"

AUTH_HAZIR=0
if [ -z "$TOKEN" ]; then
  uyar "CLI belirteci okunamadı — izinli alanı konsoldan ekle"
else
  CFG="$(curl -s "https://identitytoolkit.googleapis.com/admin/v2/projects/$PROJE/config" -H "Authorization: Bearer $TOKEN")"
  if printf '%s' "$CFG" | grep -q CONFIGURATION_NOT_FOUND; then
    uyar "Authentication henüz açılmamış — aşağıdaki adımı yapıp betiği tekrar çalıştır"
  else
    AUTH_HAZIR=1
    YENI="$(printf '%s' "$CFG" | SITE="$SITE" python3 -c "
import json, os, re, sys
d = json.loads(re.sub(r'[\\x00-\\x1f]', ' ', sys.stdin.read()))
a = d.get('authorizedDomains', [])
s = os.environ['SITE']
if s not in a: a.append(s)
print(json.dumps({'authorizedDomains': a}))
")"
    if curl -s -o /dev/null -X PATCH \
      "https://identitytoolkit.googleapis.com/admin/v2/projects/$PROJE/config?updateMask=authorizedDomains" \
      -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$YENI"; then
      tamam "$SITE izinli alanlarda"
    else
      uyar "izinli alan eklenemedi — konsoldan ekle"
    fi
  fi
fi

# ── Kapanış ─────────────────────────────────────────────────────────
if [ "$AUTH_HAZIR" = "1" ]; then
  printf "\n%s── Kurulum tamam ──%s\n" "$KALIN" "$BITIR"
  printf "  python3 scripts/build_web.py     # \"bulut açık\" yazmalı\n"
  printf "  ./deploy.sh \"Google girişi\"      # yayına al\n\n"
else
  printf "\n%s── Konsoldan yapılacak tek adım ──%s\n" "$KALIN" "$BITIR"
  printf "Google girişini açmak CLI'den yapılamıyor: Firebase bu sırada projeye bir\n"
  printf "OAuth istemcisi üretiyor ve bunun için destek e-postası seçmen gerekiyor.\n\n"
  printf "  https://console.firebase.google.com/project/%s/authentication/providers\n\n" "$PROJE"
  printf "  Authentication → Get started → Google → Enable\n"
  printf "  → Public-facing name ve Support email doldur → Save\n\n"
  printf "Sonra betiği tekrar çalıştır; izinli alanı ve gerisini kendisi halleder:\n\n"
  printf "  ./scripts/setup_firebase.sh %s\n\n" "$PROJE"
fi
