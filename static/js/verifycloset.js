"use strict";

function flashSaved(result) {
    $(`#form-${result}`).removeClass("visible").addClass("hidden");
    $(`#div-${result}`).removeClass("hidden").addClass("visible");
};

function savePieceDetails(thing) {

    let $inputs= $(`#form-${thing} :input`);

    // for creating a string with category checkboxes
    let categoryString = "";

    $(".category-field:checked").each(function() {
        categoryString += ($(this).val()) + ",";
    });

    let formInputs = {
        "desc": $(".desc-field").val(),
        "other_desc": $(".other-desc-field").val(),
        "clothing_type": $(".clothing-type-field").val(),
        "category": categoryString,
        "c_id": thing,
    };
    
    $.post("/verifycloset", formInputs, flashSaved);

};
