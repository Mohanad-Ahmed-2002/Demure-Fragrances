document.addEventListener("DOMContentLoaded", () => {
    window.addToCart = function (productId) {
        productId = parseInt(productId);

        fetch(`/ajax/add-to-cart/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(() => {
            return fetch('/api/cart-count/');
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ New cart count from server:", data.cart_count);

            // ✅ حدث كل العناصر اللي عندها class="cart-count"
            document.querySelectorAll(".cart-count").forEach(badge => {
                badge.textContent = data.cart_count;
                badge.classList.remove("hidden");

                // Animation (اختياري)
                badge.classList.add("scale-110");
                setTimeout(() => badge.classList.remove("scale-110"), 300);
            });
        })
        .catch(error => {
            console.error("❌ Error updating cart count:", error);
        });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            for (let cookie of document.cookie.split(';')) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ✅ أظهر العدّاد مباشرة لو cart_count > 0 عند تحميل الصفحة
    document.querySelectorAll(".cart-count").forEach(badge => {
        if (parseInt(badge.textContent) > 0) {
            badge.classList.remove("hidden");
        }
    });
});
