import requests


class BreakFast(object):
	url = 'https://breakfastapi.fun'
	
	def __init__(
			self,
			id: int,
			name: str,
			duration: int,
			ingredients: set | list | tuple,
			directions: str):
		
		self.id = id
		self.name = name
		self.duration = duration
		self.ingredients = ingredients
		self.directions = directions
	
	def copy(self):
		z = self.__dict__
		z["total_duration"] = z["duration"]
		
		return self.from_json(z)
	
	@classmethod
	def from_json(cls, json: dict):
		if "status" in set(json.keys()):
			json = json["recipe"]
		
		breakfast = cls(
			json["id"],
			json["name"],
			json["total_duration"],
			json["ingredients"],
			json["directions"]
		)
		
		return breakfast
	
	@classmethod
	def from_response(cls, response: requests.Response):
		json = response.json()
		return cls.from_json(json)
	
	@classmethod
	def from_request(cls, request: requests.Response):
		return cls.from_response(request)
	
	@classmethod
	def random(cls):
		return cls.from_request(requests.get(cls.url))
	
	def __hash__(self):
		return hash(tuple(vars(self).keys()))
	
	def __eq__(self, __o: object) -> bool:
		if isinstance(self, __o):
			return self.id == __o.id
		
		return False
	
	def __getitem__(self, item: str):
		return vars(self)[item]
	
	def __str__(self):
		return self.name
	
	def __int__(self):
		return self.id
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		del self
		