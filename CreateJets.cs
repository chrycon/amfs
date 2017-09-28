using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;
//*
// A JetState consists of a jetNo, the starting velocity of the jet, the
// light's color and the light's intensity
[System.Serializable]
public class JetState{
    public int jetNo;
    public float velocity;
    public Color lightColor;
    public float lightIntensity;
}
// An Interval object consists of an array of JetState objects
[System.Serializable]
public class Interval{
    //public int intervalNo;
    public JetState[] jetStates;
}
// A Performance object consists of an array of Interval objects
[System.Serializable]
public class Performance{
    public Interval[] intervals;
}
//*/
public class CreateJets : MonoBehaviour{
	public GameObject jet;
    public GameObject spotlight_go;
    public int numberOfOuterCircle = 36;
    public int numberOfMiddleCircle = 36;
    public int numberOfInnerCircle = 4;
    public float radiusOuterCircle = 10f;
    public float radiusMiddleCircle = 8f;
    public float radiusInnerCircle = 2f;
	AudioSource audio;
	bool fountainStarted = false;
	public float startTime;
    public float timePassed;
	public int timeDs;
    private ParticleSystem.Particle[] particles = new ParticleSystem.Particle[2000];
    ParticleSystem particleSystem;
	Light spotlight;
    public GameObject[] jets = new GameObject[77];
    public GameObject[] lights = new GameObject[77];
    int switchLight = 0;
	Performance performance;
	bool[] sync_array = new bool[6000];
	float[] samples;

	// Start is called once when the game starts
	void Start(){
        Vector3 lightHeight = new Vector3(0f, 0f, 0.5f);
        //Build outer circle of jets
        for (int i = 0; i < numberOfOuterCircle; i++){
            float angle = i * Mathf.PI * 2 / numberOfOuterCircle;
            Vector3 pos = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle)) * radiusOuterCircle;
            Instantiate(jet, pos, Quaternion.Euler(-90,0,0));
            Instantiate(spotlight_go, pos + lightHeight, Quaternion.Euler(-90, 0, 0));

        }
        //Build middle circle of jets

        for (int i = 0; i < numberOfMiddleCircle; i++){
            float angle = i * Mathf.PI * 2 / numberOfMiddleCircle;
            Vector3 pos = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle)) * radiusMiddleCircle;
            Instantiate(jet, pos, Quaternion.Euler(-90, 0, 0));
            Instantiate(spotlight_go, pos + lightHeight, Quaternion.Euler(-90, 0, 0));

        }
        //Build inner circle of jets//
        for (int i = 0; i < numberOfInnerCircle; i++){
            float angle = i * Mathf.PI * 2 / numberOfInnerCircle;
            Vector3 pos = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle)) * radiusInnerCircle;
            Instantiate(jet, pos, Quaternion.Euler(-90, 0, 0));
            Instantiate(spotlight_go, pos + lightHeight, Quaternion.Euler(-90, 0, 0));
        }
        //Build middle jet
        Instantiate(jet, new Vector3(0, 0, 0), Quaternion.Euler(-90, 0, 0));
        Instantiate(spotlight_go, new Vector3(0, 0, 0) + lightHeight, Quaternion.Euler(-90, 0, 0));
		jets = GameObject.FindGameObjectsWithTag("jets");
        lights = GameObject.FindGameObjectsWithTag("lights");
        //Parse input performance file
        string pathToInputJSON = @"Assets\Resources\performance.json";
		try{
			print("Loading JSON performance file...");
			TextAsset fileString = Resources.Load("performance") as TextAsset;
			//var fileString = (new StreamReader(Application.dataPath + "/" + "performance.json")).ReadToEnd();
			//performance = JsonUtility.FromJson<Performance>(fileString);
			performance = JsonUtility.FromJson<Performance>(fileString.text);
		} catch (System.Exception e) {
			print("Error loading performance file.");
			//UnityEditor.EditorApplication.isPlaying = false;
		}
		//Get the audio
		audio = GetComponent<AudioSource>();

		jets = GameObject.FindGameObjectsWithTag("jets");
		lights = GameObject.FindGameObjectsWithTag("lights");
// samples = new float[audio.clip.samples * audio.clip.channels];
	//	audio.clip.GetData(samples, 0);
	}

	// Update is called once per frame
    void Update(){
		// Start the fountain at the press of key 'k'
		if (Input.GetKey("k") && !fountainStarted){
			// Play the audio
			audio.Play(0);
			fountainStarted = true;
			startTime = Time.time;

		}
		if (fountainStarted) {
			timePassed = (Time.time - startTime)*10;
			timeDs=(int)timePassed;
			if (!sync_array[timeDs]) {
				//float currentSample = Mathf.Abs(samples[audio.timeSamples]);
				// For each jet and spotlight
				for (int i = 0; i < performance.intervals[timeDs].jetStates.Length; i++) {
					particleSystem = jets[i].GetComponent<ParticleSystem>();
					spotlight = lights[i].GetComponent<Light>();
					// Set the current speed of the particle system
					particleSystem.startSpeed = performance.intervals[timeDs].jetStates[i].velocity;
					// Set the color of the spotlight
					spotlight.color = performance.intervals[timeDs].jetStates[i].lightColor;
					// Set the intensity of the spotlight
					spotlight.intensity = performance.intervals[timeDs].jetStates[i].lightIntensity;
					particleSystem.Play();
					// Change the color of the particles from the current particle system based
					// on the color of the spotlight. This has to be done manually as the light
					// shader doesn't work properly
					int count = jets[i].GetComponent<ParticleSystem>().GetParticles(particles);
					for (int j = 0; j < count; j++) {
						float t = particles[j].position.z / 10f;
						particles[j].startColor = Color.Lerp(spotlight.color, new Color(1, 1, 1), t);
					}
					particleSystem.SetParticles(particles, count);
					particleSystem.startColor = spotlight.color;
				}
				sync_array[timeDs] = true;
			};
		}
	}
}
