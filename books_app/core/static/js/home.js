var modal_mode = 'create';
var update_id_book = '';
$(document).ready(function() {
    $('#form-modal').on('submit', function(e) {
        e.preventDefault();
        data = {
            title: document.getElementById('book_title').value,
            author: document.getElementById('book_author').value,
            num_pages: document.getElementById('book_num_pages').value,
            gender: document.getElementById('book_gender').value,
            status: document.getElementById('book_status').value,
            score: document.getElementById('book_score_select').value,
        }

        if (modal_mode == 'create') {
            $.ajax({
                type: "POST",
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                },
                url: '/api/books/',
                data: data,
                success: function(response) {
                    document.location.reload(true);
                },
                error: function(response) {

                    alert('Error adding book!')
                },
                dataType: 'json'
            });
        } else {
            $.ajax({
                type: "PUT",
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                },
                url: '/api/books/' + update_id_book + '/',
                data: data,
                success: function(response) {
                    document.location.reload(true);
                },
                error: function(response) {
                    alert('Error editing book!')
                },
                dataType: 'json'
            });
        }
    });

    $('#form-modal-book-gender-edit').on('submit', function(e) {
        e.preventDefault();
        book_gender_id = document.getElementById('book_gender_edit_select').value

        data = {
            id: book_gender_id,
            name: document.getElementById('book_gender_new_name').value
        }

        $.ajax({
            type: "PUT",
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            url: '/api/book-gender/' + book_gender_id + '/',
            data: data,
            success: function(response) {
                document.location.reload(true);
            },
            error: function(response) {
                alert('Error editing book gender!')
            },
            dataType: 'json'
        });

    })

});

function resetModal() {
    modal_mode = "create"
    document.getElementById('book_title').value = ''
    document.getElementById('book_author').value = ''
    document.getElementById('book_num_pages').value = ''
    $("#book_gender").val('').trigger('change');
    $("#book_status").val('').trigger('change');
    $("#book_score_select").val('').trigger('change');
    $("#book_score_select").disabled = true;
    document.getElementById('modal-btn').textContent = 'Add'
    document.getElementById('modal-title').textContent = 'Add book'

}

function updateModal(book_id) {
    update_id_book = book_id;
    modal_mode = 'edit';
    $("#book_score_select").disabled = false
    document.getElementById('modal-title').textContent = 'Edit book'
    document.getElementById('modal-btn').textContent = 'Edit'

    $.ajax({
        type: "GET",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        url: '/api/books/' + book_id + '/',
        success: function(response) {
            document.getElementById('book_title').value =
                response.title
            document.getElementById('book_author').value =
                response.author
            document.getElementById('book_num_pages').value =
                response.num_pages

            book_gender = response.gender
            if (book_gender == null) {
                $("#book_gender").val('').trigger('change');
            } else {
                $("#book_gender").val(response.gender).trigger('change');
            }

            $("#book_status").val(response.status).trigger('change');

            if (response.status == 'COMPLETED') {
                $("#book_score_select").val(response.score).trigger('change');
            } else {
                $("#book_score_select").val('').trigger('change');
                $("#book_score_select").disabled = true;
            }
        },
        error: function(response) {
            alert('Error editing book!')
        },
        dataType: 'json'
    });

}

function deleteBook(book_id) {
    $.ajax({
        type: "DELETE",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        url: '/api/books/' + book_id + '/',
        success: function(response) {
            alert('Book deleted!')
            document.location.reload(true);
        },
        error: function(response) {
            alert('Error deleting book!')
        },
        dataType: 'json'
    });
}

function deleteGender() {
    var book_gender_id = ''
    book_gender_id =
        document.getElementById('book_gender_edit_select').value
    $.ajax({
        type: "DELETE",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        url: '/api/book-gender/' + book_gender_id + '/',
        success: function(response) {
            alert('Book gender deleted!')
            document.location.reload(true);
        },
        error: function(response) {
            alert('Error deleting book gender!')
        },
        dataType: 'json'
    });
}

function performLogout() {
    $.ajax({
        type: "POST",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        url: '/api/user/logout/',
        success: function(response) {
            window.location.href = "/home";
        },
        error: function(response) {
            if (response.status != 200) {
                alert('Error during logout!')
            } else {
                window.location.href = "/";
            }
        },
        dataType: 'json'
    });
}

function changeStatus() {
    var status = document.getElementById('book_status').value
    if (status == 'COMPLETED') {
        document.getElementById('book_score_select').disabled = false
    } else {
        document.getElementById('book_score_select').disabled = true
        $("#book_score_select").val('').trigger('change')
    }
}

$(document).ready(function() {
    $('#form-modal-book-gender').on('submit', function(e) {

        e.preventDefault();
        data = {
            name: document.getElementById('book_gender_name').value,
        }
        $.ajax({
            type: "POST",
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            url: '/api/book-gender/',
            data: data,
            success: function(response) {
                document.location.reload(true);
            },
            error: function(response) {

                alert('Error adding book gender!')
            },
            dataType: 'json'
        });
    });
});

function performFiltering() {
    var status_filter =
        document.getElementsByClassName('filter_status')[0].value
    var gender_filter =
        document.getElementsByClassName('filter_gender')[0].value

    var URL = '/api/books?'
    if (status_filter != '') {
        URL += 'status=' + status_filter
    }
    if (gender_filter != '') {
        if (status_filter != '') {
            URL += '&gender=' + gender_filter
        } else {
            URL += 'gender=' + gender_filter
        }
    }
    var book_genders = []
    $.ajax({
        type: "GET",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        url: '/api/book-gender/',
        success: function(response) {
            book_genders = response
        },
        error: function(response) {
            alert('Error filtering books!')
        },
        dataType: 'json'
    });

    $.ajax({
        type: "GET",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        url: URL,
        success: function(response) {

            response.forEach((book) => {
                book.status = book.status.replaceAll('_', ' ')
                book.status = book.status.charAt(0) + book.status.slice(1).toLowerCase();
                book.gender_name = '---'
                if (book.score == null) {
                    book.score = '---'
                }
                book_genders.forEach((book_gender) => {
                    if (book.gender == book_gender.id) {
                        book.gender_name = book_gender.name
                    }
                })
            })

            table_body = document.getElementById('book-table-body')
            table_body.innerHTML = ''
            if (response.length > 0) {
                var new_table_body = ''
                response.forEach((book) => {
                    var table_row = '<tr>'
                    table_row = table_row + '<td>' + book.title + '</td>'
                    table_row = table_row + '<td>' + book.author + '</td>'
                    table_row = table_row + '<td>' + book.gender_name + '</td>'
                    table_row = table_row + '<td>' + book.num_pages + '</td>'
                    table_row = table_row + '<td>' + book.status + '</td>'
                    table_row = table_row + '<td>' + book.score + '</td>'
                    table_row =
                        table_row + '<td class="text-center"><button onClick="updateModal(' + book.id + ')" type="button" style="border: none; background-color:rgba(0, 0, 0, 0)" data-toggle="modal" data-target="#book-modal"><i class="fas fa-edit text-info"></i></button></td>'
                    table_row =
                        table_row + '<td class="text-center"><button onClick="deleteBook(' + book.id + ')" style="border: none; background-color:rgba(0, 0, 0, 0)"><i class="fas fa-minus-circle text-danger"></i></button></td>'

                    table_row = table_row + '</tr>'
                    new_table_body += table_row
                })
                table_body.innerHTML = new_table_body
                document.getElementById('filter-msg').style.display =
                    'none'
            } else {
                document.getElementById('filter-msg').style.display =
                    'block'
            }
        },
        error: function(response) {
            alert('Error filtering books!')
        },
        dataType: 'json'
    });
}

$(document).ready(function() {
    $('.filter_status').select2({
        width: '200px',
        placeholder: "Filter by status",
        minimumResultsForSearch: -1,
        initSelection: function(element, callback) {}
    });

    $('#book_gender').select2({
        width: '200px',
        placeholder: "Select a gender",
        minimumResultsForSearch: -1,
        initSelection: function(element, callback) {}
    });

    $('#book_status').select2({
        width: '200px',
        placeholder: "Select a status",
        minimumResultsForSearch: -1,
        initSelection: function(element, callback) {}
    });

    $('#book_score_select').select2({
        width: '200px',
        placeholder: "Select a score",
        minimumResultsForSearch: -1,
        initSelection: function(element, callback) {}
    });

    $('#book_gender_edit_select').select2({
        width: '200px',
        placeholder: "Select a gender",
        minimumResultsForSearch: -1,
        initSelection: function(element, callback) {}

    });

    $('#book_gender_edit_select').on('change', () => {
        document.getElementById('modal-delete-gender-btn').disabled = false
    })

    $('.filter_gender').select2({
        width: '200px',
        placeholder: "Filter by book gender",
        minimumResultsForSearch: -1,
        initSelection: function(element, callback) {}
    });
});