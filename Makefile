format:
	uv tool run ruff@0.9 check --fix && uv tool run ruff@0.9 format

generate_sales_data:
	uv run code/sales_data_generator.py

run_sales_agent:
	uv run code/sales.py

run_minirag:
	uv run code/minirag.py

run_phoenix:
	@if [ "$$(docker ps -aq -f name=phoenix)" ]; then \
		docker start phoenix; \
	else \
		docker run --name phoenix -d -p 6006:6006 -p 4317:4317 -i -t arizephoenix/phoenix:latest; \
	fi

stop_phoenix:
	docker stop phoenix

