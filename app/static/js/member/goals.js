function toggleProofs(id) {
    var proofs_list = $("#" + id);
    if (proofs_list.is(":hidden")) {
        proofs_list.show("fast");
    } else {
        proofs_list.slideUp();
    }
}

function openProofModal(text, step_name, goal_name, documentName) {
    $("#proofModal").modal('show');
    $("#upload_proof_name").html(text);
    $("#proof_file").val(null);
    $("#proof_name").val(text);
    $("#step_name").val(step_name);
    $("#goal_name").val(goal_name)
}

function closeProofModal() {
    $("#proofModal").modal('hide');
}

function saveProof() {
    $("#upload-proof-form").submit();
    closeProofModal();
}

function changeGoalOptions(e) {
    var curCat;
    var html;
    $(".goal-option").attr("hidden", false);
    $(".goal-option").addClass("goal-option-hide")
    curCat = $(e).val();
    $("." + curCat + "-option").removeClass("goal-option-hide");
    $(".goal-option-hide").attr("hidden", true);
    html = $(".goal-option").not(".goal-option-hide").first().html();
    $("#goal-name-select").val(html);
}

function addMemberGoal() {
    goalName = $("#goal-name-select").val();
    $.post( "goals/add_goal", {'goal_name':goalName}, function() {
      console.log( "successfully requested to add goal" );
      })
      .done(function(data) {
        if (data.success == false) {
            window.alert(data.error);
        } else {
            window.location.reload();
        }
      })
      .fail(function(err) {
        console.log(err);
      });
}