

function delModal(sn_id, loc){
  $('#confirmmodal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    if(button[0].id=="id_deleteselection"){
      var  data=getSelectValues('selection');
    }
    else{
      var data = [button.data('id')];
    }
    var modal=$(this);
    var link=document.getElementById('id_deleteform');
    link.setAttribute('action', '/sn/'+sn_id+'/'+loc+'/delete/');
    document.getElementById('id_idlist').setAttribute('value', data)
  });
}

function getSelectValues(checkboxName) {
  var checkboxes = document.querySelectorAll('input[name="' + checkboxName + '"]:checked'), values = [];
    Array.prototype.forEach.call(checkboxes, function(el) {
        values.push(el.value);
    });
    return values;
};
