import os

archivo = "index.html"

if not os.path.exists(archivo):
    print("❌ Error: No estás en la carpeta correcta o no existe index.html")
    exit()

# Hacemos una copia de seguridad por si algo sale mal
os.system(f"cp {archivo} {archivo}.bak")

with open(archivo, "r", encoding="utf-8") as f:
    html = f.read()

# 1. El código de Meeus y la lógica de la Luna
codigo_js = """
<script>
// ==========================================
// MOTOR ASTRONÓMICO 5D - VERDAD CRUDA (Meeus)
// ==========================================
const julianDateFromUnixTime = (t) => (t / 86400000) + 2440587.5;
const constrainAngle = (degrees) => {
    let t = degrees % 360;
    if (t < 0) t += 360;
    return t;
}
const radiansPerDegree = Math.PI / 180.0;

const phaseAngleDegrees = (jd) => {
    const T = (jd - 2451545) / 36525.0;
    const tSquared = T * T;
    const tCubed = tSquared * T;
    const tToTheFour = tCubed * T;
    const D = constrainAngle(297.8501921 + 445267.1114034 * T - 0.0018819 * tSquared + 1.0/545868.0 * tCubed - 1.0/113065000.0 * tToTheFour) * radiansPerDegree;
    const M = constrainAngle(357.5291092 + 35999.0502909 * T - 0.0001536 * tSquared + 1.0/24490000.0 * tCubed) * radiansPerDegree;
    const Mp = constrainAngle(134.9633964 + 477198.8675055 * T + 0.0087414 * tSquared + 1.0/69699.0 * tCubed - 1.0/14712000.0 * tToTheFour) * radiansPerDegree;
    return constrainAngle(180 - D*180/Math.PI - 6.289 * Math.sin(Mp) + 2.1 * Math.sin(M) -1.274 * Math.sin(2*D - Mp) -0.658 * Math.sin(2*D) -0.214 * Math.sin(2*Mp) -0.11 * Math.sin(D));
}

function actualizarVerdadCruda() {
    const jd = julianDateFromUnixTime(Date.now());
    const angle = phaseAngleDegrees(jd);
    const fraction = (1 + Math.cos(angle * radiansPerDegree)) / 2; 
    
    const T = (jd - 2451545) / 36525.0;
    let L = 218.316 + 13.176396 * (jd - 2451545);
    let Lp = 134.963 + 13.064993 * (jd - 2451545);
    let longitud = constrainAngle(L + 6.289 * Math.sin(Lp * radiansPerDegree));
    
    const mansion = Math.floor(longitud / 12.857) + 1;
    
    const hud = document.getElementById('hud-5d');
    if (hud) {
        hud.innerHTML = `MANSION LUNAR: ${mansion}<br>FASE LUNAR: ${Math.round(fraction * 100)}%`;
    }
}

// Ejecutar cada segundo
setInterval(actualizarVerdadCruda, 1000);
</script>
"""

# 2. El panel visual (HUD)
hud_html = """
<div id="hud-5d" style="position:fixed; top:70px; right:20px; background:rgba(0,0,0,0.7); border:1px solid #0ff; color:#0ff; padding:10px; font-family:monospace; font-size:12px; text-align:right; z-index:9999; box-shadow: 0 0 10px #0ff;">
    CALCULANDO...
</div>
"""

# Inyectar el HUD antes de cerrar el body
if "</body>" in html:
    html = html.replace("</body>", hud_html + "\n</body>")
else:
    html += hud_html

# Inyectar el JS antes de cerrar el html
if "</html>" in html:
    html = html.replace("</html>", codigo_js + "\n</html>")
else:
    html += codigo_js

with open(archivo, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ ¡Inyección completada con éxito!")
print("✅ Se ha creado un respaldo en index.html.bak")
print("👉 Ahora sube los cambios a GitHub:")
print("   git add index.html")
print("   git commit -m 'Motor Meeus 5D inyectado'")
print("   git push origin main")
