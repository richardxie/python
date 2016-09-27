define([
  'text!templates/Home.html',
  'text!templates/Data.html',
  'text!templates/Signin.html'
],function(homeTemplate,dataTemplate, signinTemplate){
  return {
    home: {
      title: 'Home'
      , route: '/home'
      , controller: 'home'
      , template: homeTemplate
    }
    , creation: {
      title: 'Data List'
      , route: '/data'
      , controller: 'data'
      , template: dataTemplate
    }
    , signin: {
      title: '签到情况'
      , route: '/signin'
      , controller: 'signin'
      , template: signinTemplate
    }
  };
})
