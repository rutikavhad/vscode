const upload = document.getElementById("upload");
const gallery = document.getElementById("gallery");
const slideBtn = document.getElementById("slideshowSelected");
const slideTimeInput = document.getElementById("slideTime");

const slideshowQueue = document.getElementById("slideshowQueue");
const clearQueueBtn = document.getElementById("clearQueue");

const loadJsonBtn = document.getElementById("loadJsonBtn");
const jsonInput = document.getElementById("jsonInput");

const preview = document.getElementById("preview");
const previewImg = document.getElementById("previewImg");

let photos = [];
let queue = [];

/* Resize & Compress Image */
function compressImage(file, callback) {
  const reader = new FileReader();
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      const canvas = document.createElement("canvas");
      const maxWidth = 800;
      const scale = maxWidth / img.width;

      canvas.width = maxWidth;
      canvas.height = img.height * scale;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      callback(canvas.toDataURL("image/jpeg", 0.7));
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

/* Upload Images */
upload.addEventListener("change", e => {
  [...e.target.files].forEach(file => {
    compressImage(file, (compressed) => {
      photos.push(compressed);
      renderGallery();
    });
  });
});

/* Render Gallery */
function renderGallery() {
  gallery.innerHTML = "";

  photos.forEach(src => {
    const card = document.createElement("div");
    card.className = "photo-card";

    const img = document.createElement("img");
    img.src = src;

    img.onclick = () => {
      queue.push(src);
      renderQueue();
    };

    img.oncontextmenu = (e) => {
      e.preventDefault();
      previewImg.src = src;
      preview.style.display = "flex";
    };

    card.appendChild(img);
    gallery.appendChild(card);
  });
}

/* Render Order */
function renderQueue() {
  slideshowQueue.innerHTML = "";

  queue.forEach((src, index) => {
    const img = document.createElement("img");
    img.src = src;

    img.onclick = () => {
      queue.splice(index, 1);
      renderQueue();
    };

    slideshowQueue.appendChild(img);
  });
}

clearQueueBtn.onclick = () => {
  queue = [];
  renderQueue();
};

/* Start Slideshow */
slideBtn.onclick = () => {
  if (!queue.length) {
    alert("Add images first!");
    return;
  }

  try {
    sessionStorage.removeItem("slideshowData");

    sessionStorage.setItem(
      "slideshowData",
      JSON.stringify({
        slides: queue,
        delay: slideTimeInput.value * 1000
      })
    );

    window.open("slideshow.html", "_blank");

  } catch {
    alert("Too many images selected. Please reduce amount.");
  }
};

/* Load JSON Direct Play */
loadJsonBtn.onclick = () => jsonInput.click();

jsonInput.onchange = (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();

  reader.onload = () => {
    try {
      sessionStorage.removeItem("slideshowData");
      sessionStorage.setItem("slideshowData", reader.result);
      window.open("slideshow.html", "_blank");
    } catch {
      alert("JSON file too large.");
    }
  };

  reader.readAsText(file);
};

preview.onclick = () => preview.style.display = "none";