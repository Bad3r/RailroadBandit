Rails.application.routes.draw do

	root 'application#hello'
      	get 'bandit/index' => 'bandit#index'
      	resources :bandit
      	root 'bandit#index'
end
