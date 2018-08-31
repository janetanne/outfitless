"use strict";

// FUTURE FEATURE: check to see all pieces processed, 
// then call in callback to show button to go to closet

function flashSaved(result) {
    $(`#form-${result}`).removeClass("visible").addClass("hidden");
    $(`#div-${result}`).removeClass("hidden").addClass("visible");
};

function savePieceDetails(thing) {

    // creates list of all elements in form
    let formInputs= $(`#form-${thing}`).serialize();

    $.ajax({
        type: "POST",
        url: '/verifycloset',
        data: formInputs,
        dataType: "json",
        success: flashSaved(thing)
    });

}

