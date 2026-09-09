// Helper de acceso a datos del menú.
//
// IMPORTANTE (red de contenedores): este fetch se ejecuta en el SERVIDOR de
// Next.js, es decir, DENTRO del contenedor `frontend`. Por tanto NO puede usar
// `http://localhost:8000` (eso apuntaría al propio contenedor frontend), sino
// el nombre del servicio de Docker Compose: `http://backend:8000`.
//
// - INTERNAL_API_URL  -> uso server-side (contenedor -> contenedor).
// - NEXT_PUBLIC_API_URL -> uso desde el navegador (http://localhost:8000).
const INTERNAL_API_URL =
  process.env.INTERNAL_API_URL || "http://backend:8000";

export async function getMenu() {
  const res = await fetch(`${INTERNAL_API_URL}/api/menu`, {
    // El menú puede cambiar en cualquier momento (agotados), así que no lo
    // cacheamos: pedimos datos frescos en cada carga.
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Error al cargar el menú: ${res.status}`);
  }

  return res.json();
}
