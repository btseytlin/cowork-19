function confirm_delete(post_id){
    const r = confirm("Точно удалить?");
    if (r === true) {
        console.log(post_id)
      window.location.href = "/archive/"+post_id
    }
}
