import Ember from 'ember';

export function isSolved(params/*, hash*/) {
  var challengeId = parseInt(params[0]);
  var solvedChallengeList = params[1];

  if ( solvedChallengeList.contains(challengeId)) {
    return true;
  }
  else {
    return false;
  }
}

export default Ember.Helper.helper(isSolved);
