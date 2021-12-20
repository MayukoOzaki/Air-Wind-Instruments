using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DandelionController : MonoBehaviour
{
    public GameObject topSeeds;
    public ParticleSystem ps;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if( Input.GetKeyDown(KeyCode.B) )
        {
            Blow(Vector3.forward);
        }
    }

    public void Blow(Vector3 dir)
    {
        StartCoroutine(RemoveTop());
        Vector3 target = topSeeds.transform.position + dir;
        target.y = topSeeds.transform.position.y;

        ps.transform.LookAt(target);
        ps.Play();
    }

    IEnumerator RemoveTop()
    {
        yield return new WaitForSeconds(0.2f);
        topSeeds.SetActive(false);
        yield return new WaitForSeconds(0.3f);
        gameObject.SetActive(false);
    }
}
