document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('filters');
    const initialLoad = document.getElementById('initial_load').value === 'true';

    if (initialLoad) {
        send_query();
        document.getElementById('initial_load').value = 'false';
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
       send_query();
    });

  const searchButton = document.getElementById('search_button');
    searchButton.addEventListener('click', function(event) {
        event.preventDefault();
        send_query();
    });

    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            send_query();
        });
    });
});


function send_query() {
    console.log("send query...");

    document.getElementById('results').innerHTML = '';
    document.getElementById("results_not_found").style.display = "none";
    console.log("hide not found icon");

        const searchCriteria = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        date_from: document.getElementById('date_from').value,
        date_to: document.getElementById('date_to').value,
        size_from: document.getElementById('size_from').value,
        size_to: document.getElementById('size_to').value,
      //  format: document.getElementById('format').value,
        files_count: document.getElementById('files_count').value,
        publication_type: document.getElementById('publication_type').value,
        sorting: document.getElementById('sorting').value
    };

    fetch('/explore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchCriteria),
    })
    .then(response => response.json())
    .then(data => {
        const results = document.getElementById('results');
        results.innerHTML = '';

        const resultCount = data.length;
        const resultText = resultCount === 1 ? 'dataset' : 'datasets';
        const resultsNumber = document.getElementById('results_number');
        if (resultsNumber) {
            resultsNumber.textContent = `${resultCount} ${resultText} found`;
        }

        if (resultCount === 0) {
            console.log("show not found icon");
            document.getElementById("results_not_found").style.display = "block";
        } else {
            document.getElementById("results_not_found").style.display = "none";
        }

        data.forEach(dataset => {
            let card = document.createElement('div');
            card.className = 'col-12';
            card.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex align-items-center justify-content-between">
                            <h3><a href="${dataset.url}">${dataset.title}</a></h3>
                            <div>
                                <span class="badge bg-primary" style="cursor: pointer;" onclick="set_publication_type_as_query('${dataset.publication_type}')">${dataset.publication_type}</span>
                            </div>
                        </div>
                        <p class="text-secondary">${formatDate(dataset.created_at)}</p>
                        <div class="row mb-2">
                            <div class="col-md-4 col-12">
                                <span class=" text-secondary">Description</span>
                                <p class="card-text">${dataset.description}</p>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-md-4 col-12">
                                <span class=" text-secondary">Authors</span>
                                <div class="col-md-8 col-12">
                                    ${dataset.authors.map(author => `
                                        <p class="p-0 m-0">${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}</p>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-md-4 col-12">
                                <span class=" text-secondary">Tags</span>
                                <div class="col-md-8 col-12">
                                    ${dataset.tags.map(tag => `<span class="badge bg-primary me-1" style="cursor: pointer;" onclick="set_tag_as_query('${tag}')">${tag}</span>`).join('')}
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-4 col-12"></div>
                            <div class="col-md-8 col-12">
                                <a href="${dataset.url}" class="btn btn-outline-primary btn-sm" id="search" style="border-radius: 5px;">View dataset</a>
                                <a href="/dataset/download/${dataset.id}" class="btn btn-outline-primary btn-sm" id="search" style="border-radius: 5px;">Download (${dataset.total_size_in_human_format})</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            results.appendChild(card);
        });
    });
}

function formatDate(dateString) {
    const options = {day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric'};
    const date = new Date(dateString);
    return date.toLocaleString('en-US', options);
}

function set_tag_as_query(tagName) {
    const queryInput = document.getElementById('title');
    queryInput.value = tagName.trim();
    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
}

function set_publication_type_as_query(publicationType) {
    const publicationTypeSelect = document.getElementById('publication_type');
    for (let i = 0; i < publicationTypeSelect.options.length; i++) {
        if (publicationTypeSelect.options[i].text === publicationType.trim()) {
            // Set the value of the select to the value of the matching option
            publicationTypeSelect.value = publicationTypeSelect.options[i].value;
            break;
        }
    }
    publicationTypeSelect.dispatchEvent(new Event('input', {bubbles: true}));
}

document.getElementById('clear-filters').addEventListener('click', clearFilters);

function clearFilters() {
    // Reset the search query
    let queryInput = document.querySelector('title');
    queryInput.value = "";
    // queryInput.dispatchEvent(new Event('input', {bubbles: true}));

    // Reset the author
    let authorInput = document.getElementById('author');
    authorInput.value = "";
  
    // Reset the date range
    let dateFromInput = document.getElementById('date_from');
    dateFromInput.value = "";
    let dateToInput = document.getElementById('date_to');
    dateToInput.value = "";
  
    // Reset the size range
    let sizeFromInput = document.getElementById('size_from');
    sizeFromInput.value = "";
    let sizeToInput = document.getElementById('size_to');
    sizeToInput.value = "";
  
    // Reset the files count
    let filesCountInput = document.getElementById('files_count');
    filesCountInput.value = "";
    // Reset the publication type to its default value
    if (document.getElementById('publication_type')) {
        let publicationTypeSelect = document.getElementById('publication_type');
        publicationTypeSelect.value = "any"; // replace "any" with whatever your default value is
        // publicationTypeSelect.dispatchEvent(new Event('input', {bubbles: true}));
    }
    // Reset the sorting option
    let sortingOptions = document.querySelectorAll('[name="sorting"]');
    sortingOptions.forEach(option => {
        option.checked = option.value == "newest"; // replace "default" with whatever your default value is
        // option.dispatchEvent(new Event('input', {bubbles: true}));
    });

    // Perform a new search with the reset filters
    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
    send_query();
}

document.addEventListener('DOMContentLoaded', () => {
    let urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');

    if (queryParam && queryParam.trim() !== '') {
        const queryInput = document.getElementById('title');
        queryInput.value = queryParam;
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
        console.log("throw event");
    } else {
        const queryInput = document.getElementById('title');
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
    }
});