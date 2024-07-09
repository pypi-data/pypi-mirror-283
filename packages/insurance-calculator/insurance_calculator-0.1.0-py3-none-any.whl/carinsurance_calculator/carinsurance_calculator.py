class CarInsuranceCalculator:
    def __init__(self, min_assurance, max_assurance):
        self.min_assurance = min_assurance
        self.max_assurance = max_assurance

    def calculate_assurance(self, car_value, damage_percentage):
        """
        Calculate the assurance amount based on the car's value and damage percentage.

        :param car_value: The value of the car
        :param damage_percentage: The percentage of damage (0 to 100)
        :return: The calculated assurance amount
        """
        if not (0 <= damage_percentage <= 100):
            raise ValueError("Damage percentage should be between 0 and 100")

        # Calculate base assurance amount based on damage percentage
        base_assurance = car_value * ((100 - damage_percentage) / 100)

        # Ensure the assurance amount is within the policy's min and max limits
        assurance_amount = max(self.min_assurance, min(base_assurance, self.max_assurance))

        return assurance_amount
