from gg_fpga.run import run 


if __name__ == "__main__":
    run(
        security_id=3445,
        parse_mode="p",
        duration=10000000,
        filename="parse_output.png",
        trigger_mode="h",
        price_div=100000000000
    )
