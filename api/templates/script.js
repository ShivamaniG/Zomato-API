document.addEventListener('DOMContentLoaded', function() {
    // Fetch the restaurant list
    fetch('/api/restaurants?page=1&per_page=10')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('restaurant-list');
            data.forEach(restaurant => {
                const card = document.createElement('div');
                card.className = 'col-md-4';
                card.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${restaurant['Restaurant Name']}</h5>
                            <p class="card-text">${restaurant['Address']}</p>
                            <a href="/restaurant/${restaurant['Restaurant ID']}" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                `;
                list.appendChild(card);
            });
        });

    // Fetch restaurant details if on detail page
    const path = window.location.pathname;
    const match = path.match(/\/restaurant\/(\d+)/);
    if (match) {
        const restaurantId = match[1];
        fetch(`/api/restaurant/${restaurantId}`)
            .then(response => response.json())
            .then(data => {
                const detail = document.getElementById('restaurant-detail');
                detail.innerHTML = `
                    <h2>${data['Restaurant Name']}</h2>
                    <p><strong>Address:</strong> ${data['Address']}</p>
                    <p><strong>Cuisines:</strong> ${data['Cuisines']}</p>
                    <p><strong>Average Cost for Two:</strong> ${data['Average Cost for two']} ${data['Currency']}</p>
                    <p><strong>Rating:</strong> ${data['Aggregate rating']}</p>
                `;
            });
    }
});
