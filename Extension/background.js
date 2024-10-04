chrome.extension.onRequest.addListener(function(prediction){
    
    if (prediction==1){
        alert("Warning: Malicious website detected !!");
    }else if (prediction==-1){
        alert("You are good to go!!");
    }
});