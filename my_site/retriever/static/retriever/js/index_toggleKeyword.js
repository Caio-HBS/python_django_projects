function toggleKeyword() {
    var platform = document.getElementById('id_platform');
    var keyword = document.getElementById('id_keyword');
    var keywordLabel = document.querySelector('label[for="id_keyword"]');
    if (platform.value == 'Instagram') {
      keyword.style.display = 'none';
      keywordLabel.style.display = 'none';
    } else {
      keyword.style.display = 'block';
      keywordLabel.style.display = 'block';
    }
  }
  document.getElementById('id_platform').addEventListener('change', toggleKeyword);
  toggleKeyword();