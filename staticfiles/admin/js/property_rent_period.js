document.addEventListener('DOMContentLoaded', function () {
  function toggleRentPeriod() {
    var dealType = document.getElementById('id_deal_type')
    var rentPeriodRow = document.querySelector(
      '.form-row.field-rent_period, .form-group.field-rent_period'
    )
    if (!dealType || !rentPeriodRow) return
    if (dealType.value === 'RENT') {
      rentPeriodRow.style.display = ''
    } else {
      rentPeriodRow.style.display = 'none'
    }
  }
  var dealType = document.getElementById('id_deal_type')
  if (dealType) {
    dealType.addEventListener('change', toggleRentPeriod)
    toggleRentPeriod()
  }
})
