document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("variant-data");
    const variants = JSON.parse(el.textContent);

    const productData = document.getElementById("product-data");
    const productId = productData.dataset.productId;
    const selectedVariantId = productData.dataset.selectedVariantId;

    let selectedSize = null;
    let selectedColor = null;
    let selectedFit = null;

    const initialVariant = variants.find(v => v.id === parseInt(selectedVariantId));
    if (initialVariant) {
        selectedSize = initialVariant.size;
        selectedColor = initialVariant.color;
        selectedFit = initialVariant.fit;
    }

    // Event handler: where the magic happens
    function goToVariant(newSize, newColor, newFit, doNotChangeThis) {
        const match = variants.find(v => 
            v.size === newSize &&
            v.color === newColor &&
            v.fit === newFit
        );

        if (match) {
            window.location.href = `/products/${productId}?variant=${match.id}`;
        } else {
            // if no variant with the current combination is found, choose the first that 
            // you can find with the clicked parameter -> amaz0n does this too in their app
            if (doNotChangeThis=="fit") {
                newSize=null;
                newColor=null;
            } else if (doNotChangeThis=="color") {
                newSize=null;
                newFit=null;
            } else if (doNotChangeThis=="size") {
                newFit=null;
                newColor=null;
            } else {
                newFit=null;
                newColor=null; 
                newSize =null;
            }
            const fallback = variants.find(v =>
                (newSize ? v.size === newSize : true) &&
                (newColor ? v.color === newColor : true) &&
                (newFit ? v.fit === newFit : true)
            );
            if (fallback) {
                window.location.href = `/products/${productId}?variant=${fallback.id}&notice=adjusted`;
                // remember to notify the buyer that the previous other options changed.
            } else {
                alert("No combination available for this product. Please choose another one.");
            }
        }
    }

    document.querySelectorAll(".size-option").forEach(btn => {
        btn.addEventListener("click", () => {
            const newSize = btn.dataset.size;
            goToVariant(newSize, selectedColor, selectedFit, "size");
        });
    });

    document.querySelectorAll(".color-option").forEach(btn => {
        btn.addEventListener("click", () => {
            const newColor = btn.dataset.color;
            goToVariant(selectedSize, newColor, selectedFit, "color");
        });
    });

    const fitSelect = document.querySelector(".fit-option");
    if (fitSelect) {
        fitSelect.addEventListener("change", e => {
            const newFit = e.target.value;
            goToVariant(selectedSize, selectedColor, newFit, "fit");
        });
    }
});