import Ember from 'ember';

export default Ember.Controller.extend({
  error: '',
  isvalidLogin: function(credentials){
    var teamName = credentials.teamName;
    var password = credentials.password;
    if (teamName.length === 0 || password.length === 0) {
        this.set('error', "You must enter a teamname and password");
        return false;
    }
    else {
      return true;
    }
  },
  isvalidRegister: function(registrationData){
    var teamEmail = registrationData.teamEmail;
    var teamName = registrationData.teamName;
    var password = registrationData.password;
    var confirmPassword = registrationData.confirmPassword;
    if (teamEmail.length === 0 || teamName.length === 0 || password.length === 0 || confirmPassword.length === 0) {
        this.set('error', "You must fill in all the fields of the form");
        return false;
    }
    else if (password !== confirmPassword) {
        this.set('error', "Password and Password Confirmation do not match");
        return false;
    }
    else {
      return true;
    }
  },
});
