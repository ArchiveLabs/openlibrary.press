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

      // Set display info (if you want)
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

      // Form inputs update
      const nameInput = document.getElementById("name");
      const priceInput = document.getElementById("price");
      const itemInput = document.getElementById("item");
      const filenameInput = document.getElementById("filename");

      // Name = title + " (digital book)"
      const title = edition.title || "Unknown Title";
      nameInput.value = `${title} (digital book)`;

      // Price: if unknown, default to "250"
      // Let's assume edition.price or edition.price_amount exists, otherwise fallback
      // Since Open Library data usually does not have price, we default to 250
      priceInput.value = "250";

      // Item = ia identifier (Internet Archive identifier)
      // edition.ia is the common property for IA identifier, fallback to empty string if missing
      itemInput.value = edition.ia || "";

      // Filename: default to "the-quintet_text.pdf"
      // or use first available format file from edition.formats (if available)
      // But Open Library editions usually do not have formats info here, so just default
      filenameInput.value = "quintet_text.pdf";
    })
    .catch(err => {
      console.error("Error fetching book data:", err);
    });
});
