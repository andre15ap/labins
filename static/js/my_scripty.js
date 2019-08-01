
$(function () {

  $(".js-teste").click(function () {
    $.ajax({
      // url: '{% url "contas:mudar" %}',
      url: '/conta/mudar',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
      	alert('deu certo');
        // $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#teste").html(data.html);
      }
    });
  });

});