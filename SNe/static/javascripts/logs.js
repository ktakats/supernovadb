function changeColorObs() {
    document.getElementById("id_obs").className = "changecolor";
    document.getElementById("id_phot").className = "";
    document.getElementById("id_spec").className = "";
}

function changeColorPhot() {
    document.getElementById("id_obs").className = "";
    document.getElementById("id_phot").className = "changecolor";
    document.getElementById("id_spec").className = "";
}
function changeColorSpec() {
    document.getElementById("id_obs").className = "";
    document.getElementById("id_phot").className = "";
    document.getElementById("id_spec").className = "changecolor";
}

function changeColorDefault() {
    document.getElementById("id_obs").className = "";
    document.getElementById("id_phot").className = "";
    document.getElementById("id_spec").className = "";
}


function init(){
  var current=window.location.pathname.slice(0,-1);
  var index = current.lastIndexOf("/");
  var logName = current.substr(index+1);
  if(logName=="obslog"){
    changeColorObs();
  }
  else if (logName=="photometry"){
    changeColorPhot();
  }
  else if (logName=="spectroscopy"){
    changeColorSpec();
  }
  else{
    changeColorDefault();
  }

}

window.onload=init();