document.addEventListener("DOMContentLoaded", () => {
const buttons = document.querySelectorAll(".add-to-cart");

buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const productId = button.dataset.productId;

        console.log("Producto añadido:", productId);

        button.textContent = "Añadido";
    });
});


});