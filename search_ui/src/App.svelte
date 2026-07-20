<script>
  import { onMount } from "svelte";
  import { liteClient as algoliasearch } from "algoliasearch/lite";
  import instantsearch from "instantsearch.js";
  import {
    clearRefinements,
    configure,
    currentRefinements,
    hierarchicalMenu,
    hits,
    pagination,
    rangeInput,
    refinementList,
    searchBox,
    stats,
    toggleRefinement
  } from "instantsearch.js/es/widgets";

  const ALGOLIA_APP_ID = "HRWDO0NBSX";
  const ALGOLIA_SEARCH_API_KEY = "2b06469b82c1b065c74b53f27cad6d9a";
  const ALGOLIA_INDEX_NAME = "products";

  let searchBoxContainer;
  let hitsContainer;

  let categoryContainer;
  let brandContainer;
  let priceContainer;
  let freeShippingContainer;
  let statsContainer;
  let currentRefinementsContainer;
  let clearRefinementsContainer;
  let paginationContainer;

  onMount(() => {
    const searchClient = algoliasearch(
      ALGOLIA_APP_ID,
      ALGOLIA_SEARCH_API_KEY
    );

    const search = instantsearch({
      indexName: ALGOLIA_INDEX_NAME,
      searchClient
    });

    search.addWidgets([
      searchBox({
          // TEXT SEARCH
          // Searches the index while the user types.
          // Searchable attributes, typo tolerance, ranking, and searchable attributes are configured
          // in the Algolia index (https://dashboard.algolia.com/apps/{ALGOLIA_APP_ID}/explorer/configuration/products/searchable-attributes);
          // placeholder and search-as-you-type behavior are
          // configured on this widget.
          // Docs: https://www.algolia.com/doc/api-reference/widgets/search-box/js
        container: searchBoxContainer,
        placeholder: "Search products..."
      }),


      configure({
          // SEARCH PARAMETERS
          // Increase hitsPerPage to show more products per page.
          // Add other configurations such as maxValuesPerFacet, etc
          // Docs: https://www.algolia.com/doc/api-reference/widgets/configure/js
        hitsPerPage: 12,
        distinct: true
      }),


      hierarchicalMenu({
          // HIERARCHICAL CATEGORY NAVIGATION
          // Lets users move through the product category tree from broad to specific.
          // Every hierarchy level must be configured as an attribute for faceting in
          // the Algolia index. limit and showMoreLimit control the visible menu size.
          // Docs: https://www.algolia.com/doc/api-reference/widgets/hierarchical-menu/js
        container: categoryContainer,
        attributes: [
          "hierarchicalCategories.lvl0",
          "hierarchicalCategories.lvl1",
          "hierarchicalCategories.lvl2",
          "hierarchicalCategories.lvl3"
        ],
        limit: 8,
        showMore: true,
        showMoreLimit: 20
      }),

      refinementList({
          // BRAND FACET
          // Lets users filter the current result set by brand(s)
          // "brand" must be configured as searchable(brand) in attributesForFaceting
          // for the facet search box to work.
          // limit, showMoreLimit, and sortBy can be adjusted for larger catalogs.
          // Docs: https://www.algolia.com/doc/api-reference/widgets/refinement-list/js
        container: brandContainer,
        attribute: "brand",
        limit: 8,
        showMore: true,
        showMoreLimit: 20,
        searchable: true,
        searchablePlaceholder: "Search brands..."
      }),

      rangeInput({
        // PRICE FILTER
        // Lets users supply minimum and maximum prices.
        // "price" must contain numbers and be configured as an attribute for
        // faceting. Optional min, max for filtering.
        // Docs: https://www.algolia.com/doc/api-reference/widgets/range-input/js
        container: priceContainer,
        attribute: "price",
        precision: 2
      }),

      toggleRefinement({
          // BOOLEAN SHIPPING FILTER
          // Applies an on/off filter to show only products with free shipping.
          // "free_shipping" must be configured as an attribute for faceting.
          // The on and off options can be changed when the indexed values aren't
          // standard true/false booleans.
          // Docs: https://www.algolia.com/doc/api-reference/widgets/toggle-refinement/js
        container: freeShippingContainer,
        attribute: "free_shipping",
        templates: {
          labelText: "Free shipping"
        }
      }),

      clearRefinements({
          // CLEAR FILTERS
          // Removes the active refinements while retaining the user's text query.
          // includedAttributes and excludedAttributes can restrict what gets cleared.
          // Docs: https://www.algolia.com/doc/api-reference/widgets/clear-refinements/js
        container: clearRefinementsContainer,
        templates: {
          resetLabel({ hasRefinements }, { html }) {
            return html`
              ${hasRefinements ? "Clear all filters" : "No filters selected"}
            `;
          }
        }
      }),

      stats({
          // RESULT STATISTICS
          // Displays information returned with the current search, eg: number of products
          // The template controls how these stats appear.
          // Docs: https://www.algolia.com/doc/api-reference/widgets/stats/js
        container: statsContainer,
        templates: {
          text(data, { html }) {
            const resultCount = data.nbHits.toLocaleString();
            const resultLabel = data.nbHits === 1 ? "product" : "products";

            return html`${resultCount} ${resultLabel}`;
          }
        }
      }),

      currentRefinements({
         // ACTIVE FILTERS
         // Displays the current category, brand, price, and shipping refinements and
         // allows users to remove them individually.
         // includedAttributes, excludedAttributes, and transformItems can be used to
         // control which refinements are shown and how their labels appear.
         // Docs: https://www.algolia.com/doc/api-reference/widgets/current-refinements/js
        container: currentRefinementsContainer
      }),

      hits({
          // SEARCH RESULTS
          // Renders products returned by Algolia.
          // The template controls presentation only
          // hitsPerPage is configured using the configure widget above.
          // Docs: https://www.algolia.com/doc/api-reference/widgets/hits/js
        container: hitsContainer,

        transformItems(items) {
          // For debugging, you can view Object IDs returned from search in browser console
          console.log(
            "Returned objectIDs:",
            items.map((item) => item.objectID)
          );

          return items;
        },
        templates: {
          item(hit, { html, components }) {
            let startsWithBrandName = false
            if (hit.brand && hit.name.startsWith(hit.brand)) {
              startsWithBrandName = true
            }

            let displayName = null;
            if (startsWithBrandName) {
              displayName = hit.name
                              .slice(hit.brand.length)
                              .replace(/^[\s-]+/, "")
            }

            const nameToDisplay = displayName || hit.name;

            return html`
              <article class="product-card">
                <div class="product-image-container">
                  <img
                    class="product-image"
                    src="${hit.image}"
                    alt="${hit.name}"
                  />
                </div>

                <div class="product-content">
                  <p class="product-brand">
                    ${components.Highlight({
                      attribute: "brand",
                      hit
                    })}
                  </p>

                  <h2 class="product-name">${nameToDisplay}</h2>

                  <div class="product-rating">
                    <span class="rating-star">★</span>
                    <strong>${hit.rating}</strong>
                    <span>/ 6</span>
                  </div>

                  <p class="product-price">$${Number(hit.price).toFixed(2)}</p>

                  <button
                    class="add-to-cart-button"
                    type="button"
                    aria-label="Add ${nameToDisplay} to cart"
                  >
                    Add to cart
                  </button>
                </div>
              </article>
            `;
          },

          empty(results, { html }) {
            return html`
              <p>No products found for <q>${results.query}</q>.</p>
            `;
          }
        }
      }),
      pagination({
          // PAGINATION
          // Navigates between pages.
          // padding controls how many adjacent page numbers appear
          // scrollTo returns the user to the search area.
          // The number of products per page comes from configure, hitsPerPage (above).
          // Docs: https://www.algolia.com/doc/api-reference/widgets/pagination/js
        container: paginationContainer,
        padding: 2,
        scrollTo: "#searchbox"
      })
    ]);

    search.start();

    return () => {
      search.dispose();
    };
  });
</script>


<header class="page-header">
  <div class="header-content">
    <h1>Algolia - Search demo</h1>
    <div id="searchbox" bind:this={searchBoxContainer}></div>
  </div>
</header>

<main>
<div class="search-layout">
  <aside class="filters">
      <div
        class="clear-filters"
        bind:this={clearRefinementsContainer}
      ></div>

      <section class="filter-section">
        <h2>Categories</h2>
        <div bind:this={categoryContainer}></div>
      </section>

      <section class="filter-section">
        <h2>Brands</h2>
        <div bind:this={brandContainer}></div>
      </section>

      <section class="filter-section">
        <h2>Price</h2>
        <div bind:this={priceContainer}></div>
      </section>

      <section class="filter-section">
        <h2>Shipping</h2>
        <div bind:this={freeShippingContainer}></div>
      </section>
    </aside>

    <section class="results-column">
      <div class="results-header">
        <div bind:this={statsContainer}></div>
        <div bind:this={currentRefinementsContainer}></div>
      </div>

      <div bind:this={hitsContainer}></div>

      <div
        class="pagination-container"
        bind:this={paginationContainer}
      ></div>
    </section>
  </div>
</main>
