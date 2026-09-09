import { getMenu } from "@/lib/menu";
import MenuList from "./menu-list";

// El menú depende de datos en vivo (disponibilidad): renderizado dinámico.
export const dynamic = "force-dynamic";

export default async function Home() {
  let menu = [];
  let error = null;

  try {
    menu = await getMenu();
  } catch (err) {
    error = err.message;
  }

  // Conteo real de platos para la voz Catalogue (encabezado de inventario).
  const dishCount = menu.reduce(
    (total, category) => total + category.products.length,
    0,
  );

  return (
    <div className="min-h-screen bg-paper text-ink">
      {/* Masthead N9 · edge-aligned: marca a la izquierda, meta a la derecha. */}
      <div className="border-b border-rule">
        <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-4 py-4 sm:px-6">
          <span className="text-lg font-semibold tracking-tight">Bocatini</span>
          <span className="font-mono text-xs uppercase tracking-[0.18em] text-muted">
            Quito · EC
          </span>
        </div>
      </div>

      <main className="mx-auto w-full max-w-5xl px-4 pb-20 pt-12 sm:px-6 sm:pt-16">
        {/* Encabezado Catalogue: marca + tagline + conteo. Sin gran display. */}
        <header className="mb-10 max-w-2xl sm:mb-12">
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
            La carta
          </h1>
          <p className="mt-3 text-base text-muted">
            {error
              ? "Nuestra cocina de siempre, hecha cada día."
              : dishCount > 0
                ? `${dishCount} platos, hechos cada día. Filtra por categoría o revisa la carta completa.`
                : "Nuestra cocina de siempre, hecha cada día."}
          </p>
        </header>

        {error && (
          <div className="rounded-md border border-rule bg-surface p-4 text-sm text-muted">
            No pudimos cargar el menú en este momento. Inténtalo de nuevo.
          </div>
        )}

        {!error && menu.length === 0 && (
          <p className="py-16 text-sm text-muted">
            El menú no está disponible por ahora.
          </p>
        )}

        {/* La obtención de datos vive aquí (Server Component); el filtrado
            interactivo se delega al Client Component, que recibe el menú por props. */}
        {!error && menu.length > 0 && <MenuList menu={menu} />}
      </main>

      {/* Sección Visítanos · dos columnas: ficha de contacto + mapa embebido.
          El <iframe> de Google Maps usa loading="lazy" para no penalizar la
          carga inicial (se descarga solo al acercarse al viewport). */}
      <section
        aria-labelledby="visitanos"
        className="border-t border-rule bg-surface"
      >
        <div className="mx-auto w-full max-w-5xl px-4 py-14 sm:px-6">
          <header className="mb-8 max-w-xl">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-muted">
              Ubicación
            </p>
            <h2
              id="visitanos"
              className="mt-2 text-2xl font-medium tracking-tight text-ink sm:text-3xl"
            >
              Te esperamos en el local.
            </h2>
          </header>

          <div className="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
            {/* Ficha de contacto */}
            <div className="flex flex-col justify-between gap-8 rounded-lg border border-rule bg-paper p-6 sm:p-8">
              <div className="space-y-6">
                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.18em] text-muted">
                    Dirección
                  </p>
                  <address className="mt-2 text-base font-medium not-italic leading-relaxed text-ink">
                    Calle y La Isla N28-100
                    <br />
                    170129 · Quito, Ecuador
                  </address>
                </div>

                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.18em] text-muted">
                    Horario
                  </p>
                  <dl className="mt-2 space-y-1.5 text-base text-ink">
                    <div className="flex items-baseline justify-between gap-4">
                      <dt className="font-medium">Lunes a viernes</dt>
                      <dd className="font-mono text-sm tabular-nums text-muted">
                        12 – 8 p.m.
                      </dd>
                    </div>
                    <div className="flex items-baseline justify-between gap-4">
                      <dt className="font-medium">Sábado</dt>
                      <dd className="font-mono text-sm tabular-nums text-muted">
                        12 – 7 p.m.
                      </dd>
                    </div>
                    <div className="flex items-baseline justify-between gap-4">
                      <dt className="font-medium">Feriados</dt>
                      <dd className="font-mono text-sm tabular-nums text-muted">
                        3 – 6/7 p.m.
                      </dd>
                    </div>
                  </dl>
                  <p className="mt-2 text-sm text-muted">
                    En feriados y días festivos atiende solo la cafetería.
                  </p>
                </div>
              </div>

              <a
                href="https://www.google.com/maps/search/?api=1&query=Bocatini+Calle+y+La+Isla+N28-100%2C+Quito"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex w-full items-center justify-center gap-2 rounded-md bg-accent px-5 py-2.5 text-sm font-medium text-accent-ink transition-colors duration-200 hover:bg-accent-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-paper"
              >
                {/* Icono de ubicación (SVG inline, sin peticiones externas) */}
                <svg
                  aria-hidden="true"
                  viewBox="0 0 24 24"
                  className="h-4 w-4"
                  fill="currentColor"
                >
                  <path d="M12 2c-3.87 0-7 3.13-7 7 0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" />
                </svg>
                Cómo llegar
              </a>
            </div>

            {/* Mapa embebido · sin API key (modo output=embed), carga diferida */}
            <div className="overflow-hidden rounded-lg border border-rule">
              <iframe
                title="Ubicación de Bocatini en Google Maps"
                src="https://maps.google.com/maps?q=Bocatini%2C%20Calle%20y%20La%20Isla%20N28-100%2C%20Quito&ll=-0.1896398,-78.501579&z=17&output=embed"
                className="block h-72 w-full sm:h-96 lg:h-full lg:min-h-[26rem]"
                style={{ border: 0 }}
                loading="lazy"
                allowFullScreen
                referrerPolicy="no-referrer-when-downgrade"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Footer Ft5 · cierre mínimo */}
      <footer className="border-t border-rule bg-surface">
        <div className="mx-auto flex w-full max-w-5xl flex-col gap-2 px-4 py-6 sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <span className="text-sm font-semibold tracking-tight text-ink">
            Bocatini
          </span>
          <span className="font-mono text-xs uppercase tracking-[0.18em] text-muted">
            Quito · EC
          </span>
        </div>
      </footer>
    </div>
  );
}
