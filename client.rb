#!/usr/bin/env ruby

require 'rubygems'

require 'pp'

#IMAGE_HOST = "192.168.56.120:8080"
IMAGE_HOST = "dd6cda073ecf.appspot.com"

image_path = ARGV[0]
name = ARGV[1]

# NOTE: httpclient's file uploads are flakey with GAE, see rest_client below
=begin
require 'httpclient'
post_to = (HTTPClient.get "http://#{IMAGE_HOST}/image/submit").body.content
puts "will upload to #{post_to}"
upload = HTTPClient.post post_to, {
  :image => File.new(image_path),
  :name => name
}
pp upload
fetch = HTTPClient.get "http://#{IMAGE_HOST}/image/#{name}.png"
pp fetch
=end

require 'rest_client'
post_to = RestClient.get "http://#{IMAGE_HOST}/image/submit"

params = { 
  :method => :post, 
  :url => post_to.to_str, 
  :payload => { 'image' => File.new(image_path), 'name' => name }
}
upload_image_response = RestClient::Request.execute(params) do |response, request, result|
   response
end
pp response

