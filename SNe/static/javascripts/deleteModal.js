

function delModal(sn_id, loc){
  $('#confirmmodal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var dataid = button.data('id');
    var modal=$(this);
    var link=document.getElementById('id_deleteform');
    link.setAttribute('action', '/sn/'+sn_id+'/'+loc+'/delete/'+dataid+'/')
  });
}
