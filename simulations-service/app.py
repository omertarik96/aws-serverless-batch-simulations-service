#!/usr/bin/env python3

from aws_cdk import core

from simulations_service.simulations_service_stack import SimulationsServiceStack


app = core.App()
SimulationsServiceStack(app, "simulations-service")

app.synth()
