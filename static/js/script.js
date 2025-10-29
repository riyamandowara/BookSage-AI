function focusSearch() {
    document.getElementById('book-search').focus();
}

// Add this to your existing JavaScript
function showRecommendButtons() {
    const searchInput = document.getElementById('book-search');
    const searchTerm = searchInput.value.trim();
    
    if (searchTerm.length > 0) {
    // Update all hidden book title fields
    document.getElementById('hybrid-book-title').value = searchTerm;
    document.getElementById('collab-book-title').value = searchTerm;
    document.getElementById('content-book-title').value = searchTerm;
    
    // Show the recommendation buttons with animation
    const buttons = document.getElementById('recommend-buttons');
    buttons.style.display = 'block';
    buttons.classList.add('animate-fadeInUp');
    
    // Add pulse animation to hybrid button (recommended)
    setTimeout(() => {
        const hybridBtn = document.querySelector('.btn-hybrid');
        hybridBtn.classList.add('animate-pulse');
    }, 1000);
    } else {
    // Shake animation for empty search
    searchInput.classList.add('animate-shake');
    setTimeout(() => {
        searchInput.classList.remove('animate-shake');
    }, 500);
    }
}


function validateSearch() {
    const searchInput = document.getElementById('book-search');
    return searchInput.value.trim().length > 0;
}

// Search autocomplete
const bookSearch = document.getElementById('book-search');
const searchResults = document.getElementById('search-results');

bookSearch.addEventListener('input', function() {
    const query = this.value.trim();
    if (query.length < 2) {
        searchResults.style.display = 'none';
        return;
    }

    fetch(`/search_books?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            searchResults.innerHTML = '';
            if (data.length > 0) {
                data.forEach(book => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.innerHTML = `
                        <div class="d-flex align-items-center">
                            <img src="${book.image_url}" style="width: 40px; height: 60px; object-fit: contain; margin-right: 10px;">
                            <div>
                                <h6 class="mb-1">${book.title}</h6>
                                <small class="text-muted">${book.author}</small>
                            </div>
                        </div>
                    `;
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        bookSearch.value = book.title;
                        searchResults.style.display = 'none';
                        
                        // Update all hidden book title fields
                        document.getElementById('hybrid-book-title').value = book.title;
                        document.getElementById('collab-book-title').value = book.title;
                        document.getElementById('content-book-title').value = book.title;
                        
                        // Show the recommendation buttons
                        document.getElementById('recommend-buttons').style.display = 'block';
                    });
                    searchResults.appendChild(item);
                });
                searchResults.style.display = 'block';
            } else {
                searchResults.style.display = 'none';
            }
        });
});

// Hide results when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.id !== 'book-search') {
        searchResults.style.display = 'none';
    }
});

// Show recommendation buttons if there's a search term (when coming back from recommendations)
document.addEventListener('DOMContentLoaded', function() {
    const searchTerm = bookSearch.value.trim();
    if (searchTerm.length > 0) {
        // Update all hidden book title fields
        document.getElementById('hybrid-book-title').value = searchTerm;
        document.getElementById('collab-book-title').value = searchTerm;
        document.getElementById('content-book-title').value = searchTerm;
        
        // Show the recommendation buttons
        document.getElementById('recommend-buttons').style.display = 'block';
    }
});

// Add this to your existing JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Animate developer cards sequentially
    const developerCards = document.querySelectorAll('.developer-card');
    developerCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
        card.classList.add('animate-fadeInUp');
});

// Tooltip for skills
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});