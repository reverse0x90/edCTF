import Ember from 'ember';

export default Ember.Component.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  teamname: '',
  password: '',
  actions: {
    collectLoginCredentials: function() {
      var teamname = this.get('teamname');
      var password = this.get('password');
      this.sendAction('creds', {'teamname': teamname, 'password': password });
    },
    openLoginModal: function() {
      this.set('isShowingLoginModal', true);
    },
    closeLoginModal: function() {
      this.set('isShowingLoginModal', false);
    },
    loginToRegisterModal: function(){
        this.set('isShowingLoginModal', false);
        this.set('isShowingRegisterModal', true);
    },
  }
});
