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

      document.getElementsByClassName("bookpage")[0].href= `https://openlibrary.org${edition.key}`;

      // Form inputs update
      const nameInput = document.getElementById("name");
      const priceInput = document.getElementById("price");
      const itemInput = document.getElementById("item");
      const olidInput = document.getElementById("olid");
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

      // Set the olid
      olidInput.value = edition.key.match(/OL(\d+)M/)?.[1];
    })
    .catch(err => {
      console.error("Error fetching book data:", err);
    });

document.getElementById('borrowButton').addEventListener('click', () => {
  const iaId = document.getElementById("item").value;
  if (iaId) {
    const iframeSrc = `https://archive.org/details/${iaId}?view=theater&wrapper=true`;
    document.getElementById("borrowIframe").src = iframeSrc;
    document.getElementById("borrowModal").classList.remove("hidden");
  }
});

document.getElementById('closeModal').addEventListener('click', () => {
  document.getElementById("borrowModal").classList.add("hidden");
  document.getElementById("borrowIframe").src = "";
});
});
