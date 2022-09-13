<script>
  function check()
  {
    var t1=document.getElementById("t1");
    var t2=document.getElementById("t2");

    var a=t1.value;
    var b=t2.value;

    var sp1=document.getElementById("sp1");
    var sp2=document.getElementById("sp2");

    if(a==null||a=="")
    {
      sp1.innerHTML="enter email";
      t1.focus();
      return false;
    }
    else if(b==null||b=="")
    {
      sp2.innerHTML="enter password";
      t2.focus();
      return false;
    }
  }
</script>