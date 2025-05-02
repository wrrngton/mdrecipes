const currentPath = window.location.pathname;
const aside = document.querySelector("aside");
const asideLinks = document.querySelectorAll("aside a");
const asideList = document.querySelector("aside ul");
const toggleMenu = document.querySelector(".menu-toggle");
const recipesJSON = document.getElementById("recipe-data");
const searchSection = document.querySelector("search");
const searchBar = document.querySelector("search input");
const searchHits = document.getElementById("hits");
const toggleSearch = document.getElementById("search-toggle");

// Add active class to active page
asideLinks.forEach((link) => {
  const linkPath = link.dataset.path;

  if (linkPath == undefined) return;

  if (linkPath == currentPath) {
    link.classList.add("aside__active");
  }
});

if (asideList.classList.contains("hidden")) {
  aside.addEventListener("click", (e) => {
    query = e.target;

    if (
      query.classList.contains("aside__category") ||
      query.classList.contains("aside__chevron")
    ) {
      const recipeList = query.classList.contains("aside__category")
        ? query.nextElementSibling
        : query.parentNode.nextElementSibling;
      recipeList.classList.toggle("hidden");
    }
  });
}

// window.addEventListener("resize", (e) => {
//   console.log(e.target.innerWidth);
//
//   if (e.target.innerWidth) {
//      aside.classList.toggle("hidden");
//   }
//
//   // aside.classList.toggle("hidden");
// });

toggleMenu.addEventListener("click", () => {
  windowWidth = window.innerWidth;

  if (windowWidth <= 1000 && !aside.classList.contains("show")) {
    aside.classList.add("show");
  }
  else if (windowWidth < 1000 && aside.classList.contains("show")) {
    aside.classList.remove("show");
    aside.classList.add("hidden");
  }
  else {
    aside.classList.toggle("hidden");
  }
});

// Search
toggleSearch.addEventListener("click", function() {
  searchSection.classList.toggle("show");
});

function renderResults(results, query) {
  if (query === "" || results.length === 0) return (searchHits.innerHTML = "");

  let html = `<ul>`;

  results.forEach((el) => {
    html += `<li>
                <article>
                  <h2><a href="/${el.category}/${el.filename}">${el.title}</a></h2>
                  <p class="tags">${el.tags.join(", ")}</p>
                </article>
              </li>`;
  });

  html += "</ul>";

  searchHits.innerHTML = html;
}

function initSearch() {
  // Create search documents
  const recipesInJSON = JSON.parse(recipesJSON.textContent);
  const recipeDocs = [];

  for (const [category, recipes] of Object.entries(recipesInJSON)) {
    for (const recipe of recipes) {
      recipeDocs.push({
        id: recipeDocs.length.toString(),
        category,
        title: recipe.title,
        tags: recipe.tags,
        filename: recipe.filename,
      });
    }
  }

  const searcher = lunr(function() {
    this.ref("id");
    this.field("category");
    this.field("title");
    this.field("tags");

    recipeDocs.forEach(function(doc) {
      this.add(doc);
    }, this);
  });

  searchBar.addEventListener("input", function(e) {
    const userQuery = e.target.value;

    const results = searcher.search(e.target.value + "*");

    const displayResults = results.map((el) => {
      const id = el.ref;
      return (item = recipeDocs.find((element) => element.id === id));
    });

    renderResults(displayResults, userQuery);
  });
}
initSearch();
