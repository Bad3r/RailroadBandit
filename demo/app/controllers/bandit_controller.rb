class BanditController < ApplicationController
    def index
        render file:  "#{Rails.root}/public/test.html"
    end
end
