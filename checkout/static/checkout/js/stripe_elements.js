// Read the keys from the JSON script tags
const publicKey = JSON.parse(document.getElementById("id_stripe_public_key").textContent);
const clientSecret = JSON.parse(document.getElementById("id_client_secret").textContent);

const stripe = Stripe(publicKey);
const elements = stripe.elements();

const style = {
    base: {
        color: "#32325d",
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
            color: "#aab7c4"
        }
    },
    invalid: {
        color: "#fa755a",
        iconColor: "#fa755a"
    }
};

// Create card element
const card = elements.create("card", { style: style });
card.mount("#card-element");

card.on("change", function(event) {
    const errorDiv = document.getElementById("card-errors");
    if (event.error) {
        errorDiv.textContent = event.error.message;
    } else {
        errorDiv.textContent = "";
    }
});


const form = document.getElementById("payment-form");
const submitButton = document.getElementById("submit-button");
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;



// submit the form
form.addEventListener("submit", function(ev) {
    console.log("funzt");
    ev.preventDefault();
    
    // Disable button and the card during the process
    submitButton.disabled = true;
    card.update({ 'disabled': true });    
    
    const saveInfoCheckbox = document.getElementById("id-save-info");
    const postData = {
        csrfmiddlewaretoken: csrfToken,
        client_secret: clientSecret,
        save_info: saveInfoCheckbox ? saveInfoCheckbox.checked : false,
        
    };

    const url = '/checkout/cache_checkout_data/'; 

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(postData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        return stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: `${form.first_name.value.trim()} ${form.last_name.value.trim()}`,
                    email: form.email.value.trim(),
                    phone: form.phone.value.trim(),
                    address: {
                        line1: form.address_line1.value.trim(),
                        line2: form.address_line2 ? form.address_line2.value.trim() : "",
                        postal_code: form.postal_code.value.trim(),
                        city: form.city.value.trim(),
                        country: form.country.value.trim(),
                    },
                },
            },
            shipping: {
                name: `${form.first_name.value.trim()} ${form.last_name.value.trim()}`,
                phone: form.phone.value.trim(),
                address: {
                    line1: form.address_line1.value.trim(),
                    line2: form.address_line2 ? form.address_line2.value.trim() : "",
                    postal_code: form.postal_code.value.trim(),
                    city: form.city.value.trim(),
                    country: form.country.value.trim(),
                },
            },
        });
    })
    .then(result => {
        if (result.error) {
            const errorDiv = document.getElementById("card-errors");
            errorDiv.innerHTML = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            `;
            submitButton.disabled = false;
            card.update({ 'disabled': false });
            document.getElementById("loading-overlay").classList.add("hidden");
        } else {
            if (result.paymentIntent.status === "succeeded") {
                form.submit();
            }
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("" + error);
        //location.reload();
    });
});