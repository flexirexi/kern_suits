(function () {
  'use strict';

  var NEW = 'NEW';
  var d = document;

  // Elements
  var selSeries   = d.getElementById('id_series_choice');
  var selProduct  = d.getElementById('id_product_choice');
  var secNewSeries  = d.getElementById('newSeriesSection');
  var secNewProduct = d.getElementById('newProductSection');

  function has(el) { return !!el; }

  function toggleSections() {
    if (has(secNewSeries) && has(selSeries)) {
      if (selSeries.value === NEW) secNewSeries.classList.remove('d-none');
      else secNewSeries.classList.add('d-none');
    }
    if (has(secNewProduct) && has(selProduct)) {
      if (selProduct.value === NEW) secNewProduct.classList.remove('d-none');
      else secNewProduct.classList.add('d-none');
    }
  }

  if (has(selSeries))  selSeries.addEventListener('change', toggleSections);
  if (has(selProduct)) selProduct.addEventListener('change', toggleSections);
  toggleSections(); // initial state

  // Upload preview + clear
  var inputImg = d.getElementById('id_new_product_image');
  var preview  = d.getElementById('imgPreview');
  var btnClear = d.getElementById('btnClearImage');

  function placeholderUrl() {
    // Prefer data-attribute; fallback to global; last resort keep current src
    return (preview && preview.getAttribute('data-placeholder')) ||
           (window.BC && window.BC.placeholderUrl) ||
           (preview ? preview.src : '');
  }

  if (has(inputImg) && has(preview)) {
    inputImg.addEventListener('change', function (e) {
      var files = e.target.files || [];
      var file = files.length ? files[0] : null;
      if (file) {
        preview.src = URL.createObjectURL(file);
      } else {
        preview.src = placeholderUrl();
      }
    });
  }

  if (has(btnClear)) {
    btnClear.addEventListener('click', function () {
      if (has(inputImg)) inputImg.value = '';
      if (has(preview)) preview.src = placeholderUrl();
    });
  }
})();
