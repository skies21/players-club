$(document).ready(function() {
    $('.add-to-cart-form[data-product-id]').on('submit', function(e) {
        e.preventDefault();

        let form = $(this);
        let url = form.attr('action');
        let data = form.serialize();
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            success: function(response) {
                if (response.message) {
                    toastr.success(response.message);
                } else if (response.error) {
                    toastr.error(response.error);
                }
            },
            error: function(xhr, errmsg, err) {
                toastr.error('Ошибка: ' + errmsg);
            }
        });
    });

    document.querySelectorAll('#add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function (event) {
            event.preventDefault();
            let url = btn.getAttribute('data-url');
            addToCart(url);
        });
    });

    function addToCart(url) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                toastr.success(data.message);
            } else if (data.error) {
                toastr.error(data.error);
            }
        })
        .catch(error => {
            toastr.error('Ошибка при добавлении в корзину. Попробуйте снова.');
        });
    }
});
