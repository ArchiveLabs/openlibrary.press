document.addEventListener('DOMContentLoaded', () => {
  fetch("https://openlibrary.org/search.json?q=author_key:OL15509317A&fields=*,editions,availability")
    .then(res => res.json())
    .then(data => {
      const work = data.docs?.[0];
      const edition = work?.editions?.docs?.[0];

      if (!edition) {
        console.error("No edition found");
        return;
      }

      document.getElementById("book-title").textContent = edition.title || "Unknown Title";
      document.getElementById("book-author").textContent = edition.author_name?.join(", ") || "Unknown Author";
      document.getElementById("publish-date").textContent = edition.publish_date?.[0] || "Unknown";
      document.getElementById("publisher").textContent = edition.publisher?.[0] || "Unknown Publisher";

      const coverId = edition.cover_i;
      if (coverId) {
        document.getElementById("book-cover").src = `https://covers.openlibrary.org/b/id/${coverId}-M.jpg`;
      } else {
        document.getElementById("book-cover").src = "https://via.placeholder.com/150x200?text=No+Cover";
      }

      document.getElementById("description").textContent = description || "No description available.";
    })
    .catch(err => {
      console.error("Error fetching book data:", err);
    });
});

