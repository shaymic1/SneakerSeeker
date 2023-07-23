from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.deployer.deployer_dkiz import DeployerDKIZ
from sneaker_seeker.deployer.deployer_singularity import DeployerSingularity
from sneaker_seeker.deployer.deployer_line import DeployerLine
from sneaker_seeker.deployer.deployer_triangle import DeployerTriangle


class DeployerFactory:
    __deployers = {"dkiz": DeployerDKIZ,
                   "singularity": DeployerSingularity,
                   "triangle": DeployerTriangle,
                   "line": DeployerLine}

    @staticmethod
    def create(deployer_type: str, **kwargs) -> Deployer:
        if deployer_type not in DeployerFactory.__deployers:
            raise ValueError(f'Invalid planner_type: {deployer_type}')
        return DeployerFactory.__deployers[deployer_type](**kwargs)

    @staticmethod
    def add_deployer(self, deployer_type: str, planner) -> None:
        DeployerFactory.__deployers[deployer_type] = planner
