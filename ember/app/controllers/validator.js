import Ember from 'ember';

export default Ember.Controller.extend({
  error: '',
  errorFields: {},
  isvalidLogin: function(credentials){
    var teamName = credentials.teamName;
    var password = credentials.password;
    if ( teamName.length === 0 ) {
      this.set('error', "Team name field cannot be blank");
      this.set('errorFields', {'teamName': true});
      return false;
    }
    else if (password.length === 0) {
      this.set('error', "Password field cannot be blank");
      this.set('errorFields', {'password': true});
      return false;
    }
    else {
      return true;
    }
  },
  invalidLogin: function(){
    this.set('error', "Team name or password invalid");
    this.set('errorFields', {'teamName': true, 'password': true});
  },
  isvalidRegister: function(registrationData){
    var email = registrationData.email;
    var teamName = registrationData.teamName;
    var password = registrationData.password;
    var confirmPassword = registrationData.confirmPassword;
    if (email.length === 0 ) {
      this.set('error', "Email field cannot be blank");
      this.set('errorFields', {'teamEmail': true});
      return false;
    }
    else if (teamName.length === 0) {
      this.set('error', "Team name field cannot be blank");
      this.set('errorFields', {'teamName': true});
      return false;
    }
    else if (password.length === 0) {
      this.set('error', "Password field cannot be blank");
      this.set('errorFields', {'password': true});
      return false;
    }
    else if (confirmPassword.length === 0) {
      this.set('error', "Password confirmation field cannot be blank");
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
  isvalidFlag: function(flag){
    if ( flag.length === 0 ) {
      this.set('error', "Flag cannot be blank");
      return false;
    }
    else {
      return true;
    }
  },
});
