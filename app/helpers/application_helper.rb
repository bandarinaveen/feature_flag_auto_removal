module ApplicationHelper

  def show_feature?(system_id = nil, flag_name)
    user = !system_id.nil? ? "PWM-" + system_id.to_s : 'test_user@abc.com'
    # LD_CLIENT.variation(flag_name, { key: user , custom: { orgId:  !system_id.nil? ? system_id : "" }}, true)
    false
  end
end
