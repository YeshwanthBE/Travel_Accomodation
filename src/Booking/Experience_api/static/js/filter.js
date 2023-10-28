document.addEventListener('DOMContentLoaded', function() {
    reviews=JSON.parse(reviews).reviews
function sortAndDisplayReviews(sortOption) {
     
    switch (sortOption) {
        case "ratinga":
            reviews.sort((a, b) => a.rating - b.rating); // Sort by rating in descending order
            break;
        case "ratingd":
            reviews.sort((a, b) => b.rating - a.rating); // Sort by rating in descending order
            break;
        case "date":
            reviews.sort((a, b) => {
                const dateA = new Date(a.datetime);
                const dateB = new Date(b.datetime);
                return dateB - dateA; // Sort by datetime in descending order (most recent first)
            });
            break;
        // Add more cases for other sorting criteria if needed
    }

    // Update the HTML to display the sorted reviews
    const reviewsContainer = document.getElementById("reviewsContainer");
    reviewsContainer.innerHTML = ""; // Clear existing reviews
    
    for (const review of reviews) {
        const reviewElement = document.createElement("div");
        reviewElement.className = "reviews";
        reviewElement.innerHTML = `
            <div class="rating">
                <h4>${review.userid}</h4>
                <h4>${review.rating}&#128970;</h4>
            </div>
            <div class="rev">
                <p>${review.review}</p>
            </div>
        `;
        reviewsContainer.appendChild(reviewElement);
    }
}
sortAndDisplayReviews("ratingd");

document.getElementById("sortByRatingButton").addEventListener("click", function () {
    sortAndDisplayReviews("ratinga");
});

document.getElementById("sortByRatingdButton").addEventListener("click", function () {
    sortAndDisplayReviews("ratingd");
});

document.getElementById("sortByDateButton").addEventListener("click", function () {
    sortAndDisplayReviews("date");
});

});
