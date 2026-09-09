"use client";

import { Fragment, useState } from "react";

function formatPrice(price) {
  // El backend envía price como número; lo mostramos siempre con 2 decimales.
  return `$${Number(price).toFixed(2)}`;
}

// Agrupa los productos de una categoría por su sub-encabezado `group`,
// preservando el orden de llegada. Los productos sin grupo (group == null)
// caen en un bloque inicial sin encabezado.
function groupProducts(products) {
  const groups = [];
  const byKey = new Map();

  for (const product of products) {
    const key = product.group ?? "";
    if (!byKey.has(key)) {
      const group = { name: product.group ?? null, items: [] };
      byKey.set(key, group);
      groups.push(group);
    }
    byKey.get(key).items.push(product);
  }

  return groups;
}

// Valor centinela para la vista inicial: muestra TODAS las categorías.
const ALL = "__all__";

export default function MenuList({ menu }) {
  // Estado del filtro. Arranca en "Todos" para que la carga inicial muestre
  // absolutamente toda la oferta sin ocultar nada.
  const [selected, setSelected] = useState(ALL);

  // Solo filtramos cuando hay una categoría concreta seleccionada; con ALL se
  // preserva el menú completo tal cual llega del servidor.
  const visible =
    selected === ALL
      ? menu
      : menu.filter((category) => category.id === selected);

  return (
    <>
      {/* Barra de filtros = navegación de secciones (N9, edge-aligned).
          Sticky: acompaña el scroll para saltar entre categorías. */}
      <nav
        aria-label="Filtrar por categoría"
        className="sticky top-0 z-20 -mx-4 mb-10 border-b border-rule bg-paper/85 px-4 py-3 backdrop-blur-sm sm:-mx-6 sm:px-6"
      >
        <div className="flex flex-wrap items-center gap-2">
          <FilterButton
            active={selected === ALL}
            onClick={() => setSelected(ALL)}
          >
            Todos
          </FilterButton>

          {menu.map((category) => (
            <FilterButton
              key={category.id}
              active={selected === category.id}
              onClick={() => setSelected(category.id)}
            >
              {category.name}
            </FilterButton>
          ))}
        </div>
      </nav>

      {/* Catálogo: rejilla responsiva de fichas de categoría, tamaños uniformes.
          grid-cols-2 de Tailwind usa minmax(0,1fr) (gate 50). */}
      <div className="grid grid-cols-1 items-start gap-px overflow-hidden rounded-md border border-rule bg-rule md:grid-cols-2">
        {visible.map((category) => (
          <section key={category.id} className="bg-surface">
            {/* Banda de categoría: etiqueta + conteo en mono (voz Catalogue). */}
            <header className="flex items-baseline justify-between gap-3 border-b border-rule px-5 py-4 sm:px-6">
              <h2 className="text-sm font-semibold uppercase tracking-[0.16em] text-ink">
                {category.name}
              </h2>
              <span className="font-mono text-xs tabular-nums text-muted">
                {category.products.length.toString().padStart(2, "0")}
              </span>
            </header>

            {category.products.length === 0 ? (
              <p className="px-5 py-6 text-sm text-muted sm:px-6">
                Sin productos disponibles.
              </p>
            ) : (
              <ul className="divide-y divide-rule">
                {groupProducts(category.products).map((group, groupIndex) => (
                  <Fragment key={group.name ?? `__ungrouped-${groupIndex}`}>
                    {/* Sub-encabezado del grupo (Café, Batidos, Recomendado…) */}
                    {group.name && (
                      <li className="bg-band px-5 py-2 sm:px-6">
                        <span className="font-mono text-[0.7rem] uppercase tracking-[0.18em] text-muted">
                          {group.name}
                        </span>
                      </li>
                    )}

                    {group.items.map((product) => (
                      <li
                        key={product.id}
                        className="flex items-baseline justify-between gap-4 px-5 py-3.5 transition-colors duration-200 hover:bg-band sm:px-6"
                      >
                        {/* Nombre del plato + nota opcional */}
                        <span className="min-w-0 [overflow-wrap:anywhere]">
                          <span className="block font-medium text-ink">
                            {product.name}
                          </span>
                          {product.description && (
                            <span className="mt-0.5 block text-sm text-muted">
                              {product.description}
                            </span>
                          )}
                        </span>
                        {/* Precio: monoespaciado, tabular, en cobalt */}
                        <span className="shrink-0 font-mono text-sm font-medium tabular-nums text-accent">
                          {formatPrice(product.price)}
                        </span>
                      </li>
                    ))}
                  </Fragment>
                ))}
              </ul>
            )}
          </section>
        ))}
      </div>
    </>
  );
}

function FilterButton({ active, onClick, children }) {
  const base =
    "rounded-md px-3.5 py-1.5 text-sm font-medium transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-paper";

  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={
        active
          ? `${base} bg-accent text-accent-ink hover:bg-accent-hover`
          : `${base} border border-rule bg-surface text-muted hover:border-accent hover:text-accent`
      }
    >
      {children}
    </button>
  );
}
