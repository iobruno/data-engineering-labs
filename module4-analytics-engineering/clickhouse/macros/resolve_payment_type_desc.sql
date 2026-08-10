{#
    Resolves the Payment Type Description based on an Id
    that varies from 1 to 6
#}

{% macro payment_desc_of(payment_type_id) -%}

case {{ payment_type_id }}
    when 1 then 'Credit Card'
    when 2 then 'Cash'
    when 3 then 'No charge'
    when 4 then 'Dispute'
    when 5 then 'Unknown'
    when 6 then 'Voided trip'
    else 'Unknown'
end

{%- endmacro %}
