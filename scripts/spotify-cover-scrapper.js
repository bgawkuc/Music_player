function download(url, filename) {
  fetch(url)
    .then(response => response.blob())
    .then(blob => {
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = document.querySelector("div.os-padding:nth-child(2) span").innerText;
      link.click();
  })
  .catch(console.error);
}

download(document.querySelector("div.os-padding:nth-child(2) img").srcset.split(/(\s+)/)[8])