import Ember from 'ember';

export default Ember.Controller.extend({
  error: '',
  isvalidLogin: function(credentials){
    var teamname = credentials.teamname;
    var password = credentials.password;
    if (teamname.length === 0 || password.length === 0) {
        this.set('error', "You must enter a teamname and password");
        return false;
    }
    else {
      return true;
    }
  },
});
