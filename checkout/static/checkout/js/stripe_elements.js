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