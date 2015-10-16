import Ember from 'ember';

export default Ember.Controller.extend({
  error: '',
  errorFields: {},
  isvalidLogin: function(credentials){
    var teamName = credentials.teamName;
    var password = credentials.password;
    if ( teamName.length === 0 ) {
      this.set('error', "Team name field can not be blank");
      this.set('errorFields', {'teamName': true});
      return false;
    }
    else if (password.length === 0) {
      this.set('error', "Password field can not be blank");
      this.set('errorFields', {'password': true});
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
    if (teamEmail.length === 0 ) {
      this.set('error', "Email field can not be blank");
      this.set('errorFields', {'teamEmail': true});
      return false;
    }
    else if (teamName.length === 0) {
      this.set('error', "Team name field can not be blank");
      this.set('errorFields', {'teamName': true});
      return false;
    }
    else if (password.length === 0) {
      this.set('error', "Password field can not be blank");
      this.set('errorFields', {'password': true});
      return false;
    }
    else if (confirmPassword.length === 0) {
      this.set('error', "Password confirmation field can not be blank");
      this.set('errorFields', {'confirmPassword': true});
      return false;
    }
    else if (password !== confirmPassword) {
        this.set('error', "Password and password confirmation do not match");
        this.set('errorFields', {'password': true, 'confirmPassword': true});
        return false;
    }
    else {
      return true;
    }
  },
});
